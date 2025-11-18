package com.babykeke.backend.repository;

import com.babykeke.backend.entity.Policy;
import com.babykeke.backend.entity.PolicyStatus;
import com.babykeke.backend.entity.PolicyType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 政策协议 Repository
 */
@Repository
public interface PolicyRepository extends JpaRepository<Policy, Integer> {

    /**
     * 查找指定类型、语言和状态的政策
     */
    @Query("SELECT p FROM Policy p WHERE p.type = :type AND p.locale = :locale AND p.status = :status ORDER BY p.effectiveAt DESC")
    List<Policy> findByTypeAndLocaleAndStatus(@Param("type") PolicyType type,
                                               @Param("locale") String locale,
                                               @Param("status") PolicyStatus status);

    /**
     * 查找最新发布的政策
     */
    @Query("SELECT p FROM Policy p WHERE p.type = :type AND p.locale = :locale AND p.status = 'published' ORDER BY p.effectiveAt DESC LIMIT 1")
    Optional<Policy> findLatestPublished(@Param("type") PolicyType type, @Param("locale") String locale);

    /**
     * 查找指定版本的政策
     */
    Optional<Policy> findByTypeAndVersionAndLocale(PolicyType type, String version, String locale);
}
